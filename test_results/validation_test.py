from Medical_system.src.file_upload.upload_manager import file_checking
from Medical_system.src.file_upload.S3_storage import file_uploading_S3


uploaded_files = [
    "temp_uploades/blood_report.pdf",
    "temp_uploades/Untitled document (18).pdf",
]

validated_files = file_checking(uploaded_files)

print("VALIDATED FILES:")
print(validated_files)

file_uploading_S3(validated_files)