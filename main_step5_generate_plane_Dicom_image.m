%% add path
clear all
addpath('/Users/zhennongchen/Documents/GitHub/Volume_Rendering_by_DL/matlab/functions')
%% get all patients
main_path = '/Volumes/McVeighLab/projects/Zhennong/AI/Zhennong_AN_dataset';
patients = Find_all_folders(main_path);
%% load the image mat data
for i = [15]
    clear twoc threec fourc metadata metadata_new
    patient_id = patients(i).name;
    disp(patient_id)
    path = [main_path,'/',patient_id,'/planes_pred_high_res_npy/',patient_id,'_LAX_collection.mat'];
    if isfile(path) ~= 1
        disp(['this patient does not have predicted planes']);
        continue
    end
    load(path)
    disp(['finish loading image'])
    
    % load dicom metadata
    dicom_folders = Find_all_folders([main_path,'/',patient_id,'/img-dcm']);
    dicom_files = dir([main_path,'/',patient_id,'/img-dcm/',dicom_folders(3).name,'/*.dcm']);
    filename = [main_path,'/',patient_id,'/img-dcm/',dicom_folders(3).name,'/',dicom_files(1).name];
    metadata = dicominfo(filename);
    disp(['finish loading metadata'])
    
    %save the plane as dicom
    save_folder = '/Users/zhennongchen/Documents/Zhennong_CT_Data/Zhennong_AN_dataset/';
    mkdir([save_folder,patient_id])
    mkdir([save_folder,patient_id,'/pred_2C'])
    mkdir([save_folder,patient_id,'/pred_3C'])
    mkdir([save_folder,patient_id,'/pred_4C'])


    for j = 1:size(twoc,3)
        metadata_new = metadata;
        metadata_new.InstanceNumber = 100 + j;
        metadata_new.RescaleIntercept = 0; % important
        % 2C 
        save_name = [save_folder,patient_id,'/pred_2C/',num2str(j),'.dcm'];
        metadata_new.SeriesDescription='pred_2C';
        metadata_new.SeriesNumber = 800 ; 
        dicomwrite(int16(flip(twoc(:,:,j)',1)),save_name,metadata_new);
        % 3C
        save_name = [save_folder,patient_id,'/pred_3C/',num2str(j),'.dcm'];
        metadata_new.SeriesDescription='pred_3C';
        metadata_new.SeriesNumber = 900 ; 
        dicomwrite(int16(flip(threec(:,:,j)',1)),save_name,metadata_new);
        % 4C
        save_name = [save_folder,patient_id,'/pred_4C/',num2str(j),'.dcm'];
        metadata_new.SeriesDescription='pred_4C';
        metadata_new.SeriesNumber = 1000 ; 
        dicomwrite(int16(flip(fourc(:,:,j)',1)),save_name,metadata_new);
    end
    disp([patient_id,' is done'])
end
