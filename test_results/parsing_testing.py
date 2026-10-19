from rag_system.parser_agent.doc_parsing import file_parsing

document = r"temp_uploades/blood_report.pdf"

results = file_parsing(document)

print(results)