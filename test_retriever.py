from types import SimpleNamespace

from app.runbook_retriever import RunbookRetriever


def test_runbook_retrieval():
    retriever = RunbookRetriever()

    test_cases = [
        {
            "name": "CPU",
            "problems": ["High CPU usage detected: 92%"],
        },
        {
            "name": "Memory",
            "problems": ["High memory usage detected: 88%"],
        },
        {
            "name": "Disk",
            "problems": ["High disk usage detected: 91%"],
        },
    ]

    print("\n========== SENTINELAI RUNBOOK RETRIEVER TEST ==========")

    passed = 0
    failed = 0

    for case in test_cases:
        incident = SimpleNamespace(problems=case["problems"])

        try:
            runbook = retriever.retrieve_runbook(incident)

            print(f"\n--- {case['name']} Runbook ---")

            if runbook and runbook != "No relevant runbook found.":
                print("PASS: Relevant runbook retrieved.")
                print(runbook)
                passed += 1
            else:
                print("FAIL: No relevant runbook found.")
                failed += 1

        except Exception as exc:
            print(f"FAIL: Error retrieving runbook: {exc}")
            failed += 1

    print("\n========== TEST SUMMARY ==========")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("RESULT: All runbook retrieval tests passed.")
    else:
        print("RESULT: Some runbook retrieval tests failed.")


if __name__ == "__main__":
    test_runbook_retrieval()