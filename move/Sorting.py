def main():
    
    ct_root = input("CT DICOM 파일 경로: ").strip('"').strip()
    mask_root = input("Pancreas 마스크 루트 폴더 경로: ").strip('"').strip()
    phase = input("PRE 할 거야 POST 할 거야: ").strip().upper()
    output_root = input("출력 경로 선택").strip()
    os.makedirs(output_root, exist_ok=True)

    for i in tqdm(range(1, 101)):
        case_id = str(i)
        ct_case_id = f"pancreas_abnormal_{case_id}"
        nii_case_id = f"pancreas_abnormal_{case_id}"
        mask_dirname = f"{phase}{case_id}.nii"

        dicom_dir = os.path.join(ct_root, ct_case_id, phase)
        mask_path = os.path.join(mask_root, nii_case_id, mask_dirname)
        output_dir = os.path.join(output_root, phase, case_id)
        os.makedirs(output_dir, exist_ok=True)

        if not os.path.exists(dicom_dir):
            print(f"DICOM 경로 없음: {dicom_dir}")
            continue
        if not os.path.exists(mask_path):
            print(f"마스크 경로 없음: {mask_path}")
            continue

        try:
            create_rtstruct_from_dicom_and_nifti(dicom_dir, mask_path, output_dir)
        except Exception as e:
            print(f"{case_id.zfill(3)}: 변환 실패 - {e}")
if __name__ == "__main__":
    main()
