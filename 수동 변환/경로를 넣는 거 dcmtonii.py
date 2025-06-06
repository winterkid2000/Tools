import os
import re
import dicom2nifti
import dicom2nifti.settings
import dicom2nifti.convert_dicom as d2n_dicom
import pydicom

def extract_patient_id(path: str) -> str:
    """경로에서 환자 번호 추출 (3자리)"""
    match = re.findall(r"\d+", path)
    return match[-1].zfill(3) if match else "000"

def convert_dicom_to_nifti_interactive():
    # 입력 경로 받기
    dicom_folder = input("DICOM 폴더 경로를 입력하세요: ").strip()

    if not os.path.isdir(dicom_folder):
        print("[X] 경로가 존재하지 않음:", dicom_folder)
        return

    ##TotalSegmentator에서 이루어진 슬라이스 간격 검증 끄기
    dicom2nifti.settings.disable_validate_slice_increment()

    ##처리 편의성을 위해 출력 파일 이름 구성
    patient_id = extract_patient_id(dicom_folder)
    phase = os.path.basename(dicom_folder).upper()  # PRE, POST 등
    output_folder = os.path.join(os.getcwd(), "converted_output")
    os.makedirs(output_folder, exist_ok=True)
    output_nii_path = os.path.join(output_folder, f"{patient_id}_{phase}.nii.gz")

    ##디버깅할 DICOM 읽기
    dcm_files = []
    for fname in os.listdir(dicom_folder):
        if fname.lower().endswith(".dcm") or '.' not in fname:
            fpath = os.path.join(dicom_folder, fname)
            try:
                dcm = pydicom.dcmread(fpath, force=True)
                dcm_files.append(dcm)
            except Exception as e:
                print(f"DICOM 파싱 실패: {fpath} - {e}")

    if not dcm_files:
        print("유효한 DICOM 파일이 없어요...")
        return

    ##변환함 
    d2n_dicom.dicom_array_to_nifti(dcm_files, output_nii_path, reorient_nifti=True)
    print(f"변환 완료: {output_nii_path}")

if __name__ == "__main__":
    convert_dicom_to_nifti_interactive()
