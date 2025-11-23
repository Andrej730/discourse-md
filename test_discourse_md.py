import subprocess


def test_extract_all_posts() -> None:
    # Same URL as in README.
    url = "https://discuss.python.org/t/pep-685-comparison-of-extra-names-for-optional-distribution-dependencies/14141/42"
    result = subprocess.run(
        ["python", "discourse_md.py", url], capture_output=True, text=True, timeout=300
    )
    assert result.returncode == 0
    lines = result.stdout.split("\n")
    title_line = lines[0]
    assert (
        title_line
        == "# PEP 685: Comparison of extra names for optional distribution dependencies"
    )
    post_lines = [line for line in lines if line.startswith("## Post")]
    assert len(post_lines) == 82
