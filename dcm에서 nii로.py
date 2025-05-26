import os
import re
import dicom2nifti
import dicom2nifti.settings
import dicom2nifti.convert_dicom as d2n_dicom
import pydicom
import nibabel as nib

def extract_patient_id(path: str) -> str:
    match = re.findall(r"\d+", path)
    return match[-1].zfill(3) if match else "000"

def convert_dicom_folder(dicom_folder: str, output_base: str, phase: str):
    if not os.path.isdir(dicom_folder):
        print(f"다이콤이 없어: {dicom_folder}")
        return

    patient_id = extract_patient_id(dicom_folder)
    output_folder = os.path.join(output_base, patient_id)
    os.makedirs(output_folder, exist_ok=True)
    output_nii_path = os.path.join(output_folder, f"{patient_id}_{phase}.nii.gz")

    dcm_files = []
    for fname in os.listdir(dicom_folder):
        if fname.lower().endswith(".dcm") or '.' not in fname:
            fpath = os.path.join(dicom_folder, fname)
            try:
                dcm = pydicom.dcmread(fpath, force=True)
                dcm_files.append(dcm)
            except Exception as e:
                print(f"다이콤이 없어: {fpath} - {e}")

    if not dcm_files:
        print(f"다이콤이 없어용: {dicom_folder}")
        return
    try:
       nifti_image = d2n_dicom.dicom_array_to_nifti(dcm_files, None, reorient_nifti=True)
       output_nii_path = output_nii_path.replace(".nii.gz", ".nii")  
       nib.save(nifti_image, output_nii_path)
       print(f"변신 완료 (.nii): {output_nii_path}")
    except Exception as e:
        print(f"변신하다가 공격 받았음: {dicom_folder} - {e}")

def batch_convert_all_patients():
    root_folder = input("다이콤 폴더 입력: ").strip('"').strip()
    phase = input("PRE/POST 입력: ").strip().upper()

    if not os.path.isdir(root_folder):
        print("다이콤이 없어:", root_folder)
        return

    if phase not in ("PRE", "POST"):
        print("PRE 아니면 POST랬지")
        return
      
    dicom2nifti.settings.disable_validate_slice_increment()

    output_base = os.path.join(os.getcwd(), "converted_output")
    os.makedirs(output_base, exist_ok=True)

    for name in sorted(os.listdir(root_folder)):
        patient_folder = os.path.join(root_folder, name)
        phase_folder = os.path.join(patient_folder, phase)
        if os.path.isdir(phase_folder):
            print(f"변신!: {phase_folder}")
            convert_dicom_folder(phase_folder, output_base, phase)

if __name__ == "__main__":
    batch_convert_all_patients()
