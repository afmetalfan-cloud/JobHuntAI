import contextlib
import copy
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

import career


class CareerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p = Path(self.tmp.name) / "candidate"
        career.init_session(self.p)
        self.data = career.load_records(career.ROOT / "examples/reference-session")

    def populate(self):
        data = copy.deepcopy(self.data)
        for i, evidence in enumerate(data["research"]["evidence"]):
            evidence["synthetic"] = False
            # Mock URLs exercise validation; tests make no web calls or claims of verification.
            evidence["url"] = f"https://source-{i}.invalid/pay"
            evidence["accessed_on"] = date.today().isoformat()
        for name, record in data.items():
            career.write_json(self.p / (name + ".json"), record)
        for stage in career.STAGES:
            for name in stage["outputs"]:
                (self.p / "outputs" / name).write_text("# Fictional test output\n\nReviewed fixture content that exercises stage completion, not real advice.\n")
        return data

    def call(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return career.main(list(args))

    def complete_through(self, last):
        for stage in career.IDS[:career.IDS.index(last) + 1]:
            self.assertEqual(self.call("complete", "--session", str(self.p), "--stage", stage, "--confirmed"), 0)

    def test_reference_valid_only_as_fictional(self):
        self.assertEqual(career.validate_records(self.data, fictional=True), [])
        self.assertTrue(any("fictional evidence" in e for e in career.validate_records(self.data)))

    def test_private_session_cannot_be_in_repository(self):
        with self.assertRaises(ValueError):
            career.session_path(career.ROOT / "private-session")
        self.assertEqual(self.call("init", "--session", str(career.ROOT / "private-session")), 1)

    def test_symlink_session_cannot_escape_policy(self):
        link = Path(self.tmp.name) / "linked-project"
        link.symlink_to(career.ROOT, target_is_directory=True)
        with self.assertRaises(ValueError):
            career.session_path(link / "candidate")

    def test_session_file_symlink_cannot_write_outside(self):
        target = Path(self.tmp.name) / "other.md"
        target.write_text("Original")
        (self.p / "next-prompt.md").symlink_to(target)
        with self.assertRaises(ValueError):
            career.next_prompt(self.p, self.data, {"completed": []})
        self.assertEqual(target.read_text(), "Original")

    def test_initialization_never_overwrites(self):
        sentinel = self.p / "keep.txt"
        sentinel.write_text("keep")
        with self.assertRaises(ValueError):
            career.init_session(self.p)
        self.assertEqual(sentinel.read_text(), "keep")

    def test_missing_claim_evidence_rejected(self):
        self.data["profile"]["claims"][0]["source_refs"] = ["invented-source"]
        self.assertTrue(any("unknown source" in e for e in career.validate_records(self.data, "interview")))

    def test_duplicate_claim_and_role_ids_rejected(self):
        self.data["profile"]["claims"].append(copy.deepcopy(self.data["profile"]["claims"][0]))
        self.data["profile"]["roles"].append(copy.deepcopy(self.data["profile"]["roles"][0]))
        errors = career.validate_records(self.data, "interview")
        self.assertTrue(any("duplicate claim" in e for e in errors))
        self.assertTrue(any("duplicate role" in e for e in errors))

    def test_estimate_requires_assumptions(self):
        self.data["profile"]["claims"][0]["estimated"] = True
        self.assertTrue(any("requires assumptions" in e for e in career.validate_records(self.data, "interview")))

    def test_malformed_records_fail_cleanly(self):
        career.write_json(self.p / "profile.json", [])
        self.assertEqual(self.call("validate", "--session", str(self.p)), 1)

    def test_confirmation_and_stage_order(self):
        self.populate()
        self.assertEqual(self.call("complete", "--session", str(self.p), "--stage", "intake"), 1)
        self.assertEqual(self.call("complete", "--session", str(self.p), "--stage", "master", "--confirmed"), 1)
        self.complete_through("intake")

    def test_all_stages_can_complete_with_reviewed_fixtures(self):
        self.populate()
        self.complete_through("action")
        state = career.read_json(self.p / "state.json")
        self.assertEqual(len(state["completed"]), 8)

    def test_edited_profile_invalidates_interview_and_downstream(self):
        data = self.populate()
        self.complete_through("roles")
        data["profile"]["claims"][0]["text"] = "Corrected participant statement"
        career.write_json(self.p / "profile.json", data["profile"])
        state = career.load_state(self.p, data)
        self.assertEqual([s["stage"] for s in state["completed"]], ["intake"])

    def test_output_edit_invalidates_approval(self):
        data = self.populate()
        self.complete_through("master")
        (self.p / "outputs/master-resume.md").write_text("Changed text that must be reviewed again.")
        state = career.load_state(self.p, data)
        self.assertEqual([s["stage"] for s in state["completed"]], ["intake", "interview", "preferences"])

    def test_missing_deliverable_blocks_completion(self):
        self.populate()
        (self.p / "outputs/intake.md").unlink()
        self.assertEqual(self.call("complete", "--session", str(self.p), "--stage", "intake", "--confirmed"), 1)

    def test_blocked_research_cannot_complete(self):
        data = self.populate()
        self.complete_through("roles")
        data["research"]["status"] = "blocked"
        data["research"]["blocked_reasons"] = ["Browsing unavailable"]
        career.write_json(self.p / "research.json", data["research"])
        self.assertEqual(self.call("complete", "--session", str(self.p), "--stage", "market", "--confirmed"), 1)

    def test_unavailable_lane_permitted_with_explanation(self):
        self.data["research"]["recommendations"][2] = {"lane": "stretch", "status": "unavailable", "reason": "No relevant evidence yet"}
        self.assertEqual(career.validate_records(self.data, fictional=True), [])

    def test_currency_and_ordered_range_required(self):
        self.data["research"]["recommendations"][0]["currency"] = "EUR"
        self.data["research"]["recommendations"][0]["target"] = 999999
        errors = career.validate_records(self.data, fictional=True)
        self.assertTrue(any("currency" in e for e in errors))
        self.assertTrue(any("low <= target <= high" in e for e in errors))

    def test_hourly_evidence_requires_annualization(self):
        self.data["research"]["evidence"][0]["basis"] = "hourly_base"
        errors = career.validate_records(self.data, fictional=True)
        self.assertTrue(any("annualization assumptions" in e for e in errors))

    def test_stale_sources_block_real_market(self):
        data = self.populate()
        data["research"]["evidence"][0]["accessed_on"] = "2000-01-01"
        self.assertTrue(any("past 30 days" in e for e in career.validate_records(data)))

    def test_resume_omits_unconfirmed_claims_and_roles(self):
        self.populate()
        self.data["profile"]["claims"][1]["confirmed"] = False
        self.data["profile"]["roles"].append({"id": "role-unconfirmed", "title": "UNVERIFIED TITLE", "employer": "Unverified employer", "start": None, "end": None, "source_refs": ["interview-1"], "confirmed": False})
        career.render_resume(self.p, self.data)
        text = (self.p / "outputs/master-resume.md").read_text()
        self.assertNotIn("Reduced repeat", text)
        self.assertNotIn("UNVERIFIED TITLE", text)
        self.assertIn("Coordinated service", text)

    def test_import_preserves_original_and_detects_change(self):
        source = Path(self.tmp.name) / "resume.txt"
        source.write_text("Private original resume")
        career.import_resume(self.p, source)
        with self.assertRaises(ValueError):
            career.import_resume(self.p, source)
        data = career.load_records(self.p)
        self.assertEqual(career.check_imports(self.p, data), [])
        (self.p / "source-resume/resume.txt").write_text("Changed original")
        self.assertTrue(career.check_imports(self.p, data))

    def test_prompt_resumes_next_stage_without_printing_candidate_data(self):
        data = self.populate()
        self.complete_through("intake")
        state = career.load_state(self.p, data)
        career.next_prompt(self.p, data, state)
        prompt = (self.p / "next-prompt.md").read_text()
        self.assertIn("Current stage: interview", prompt)
        self.assertIn("Read AGENTS.md", prompt)

    def test_all_workflow_references_and_schema_contracts_exist(self):
        for s in career.STAGES:
            self.assertTrue((career.ROOT / s["instruction"]).is_file())
        for name in career.RECORDS:
            schema = career.read_json(career.ROOT / "schemas" / (name + ".schema.json"))
            self.assertEqual(schema["type"], "object")
            self.assertTrue(schema["required"])


if __name__ == "__main__":
    unittest.main()
