package com.dapp.profileservice.common.service;

import com.dapp.profileservice.common.repository.AdminProfileRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.dapp.profileservice.common.entity.AdminProfile;
import com.dapp.profileservice.common.exception.AdminProfileNotFoundException;
import com.dapp.profileservice.common.exception.DuplicateAdminProfileExcetion;
import com.dapp.profileservice.common.mapper.AdminProfileMapper;
import com.dapp.profileservice.common.model.AdminProfileDTO;
import com.dapp.profileservice.common.model.CreateAdminProfileDTO;
import com.dapp.profileservice.common.model.UpdateAdminProfileDTO;

@Service
public class ProfileService {
    private final AdminProfileRepository adminProfileRepository;
    private final AdminProfileMapper adminProfileMapper;

    ProfileService(AdminProfileRepository adminProfileRepository, AdminProfileMapper adminProfileMapper) {
        this.adminProfileRepository = adminProfileRepository;
        this.adminProfileMapper = adminProfileMapper;
    }

    @Transactional
    public AdminProfileDTO createAdminProfile(CreateAdminProfileDTO dto) {
        adminProfileRepository.findByUserId(dto.getUserId()).ifPresent((p) -> {
            throw new DuplicateAdminProfileExcetion();
        });
        AdminProfile profile = adminProfileRepository.save(adminProfileMapper.toEntity(dto));
        return adminProfileMapper.toDto(profile);
    }

    public AdminProfileDTO getAdminProfileByUserId(Long userId) {
        return adminProfileMapper.toDto(
                adminProfileRepository.findByUserId(userId).orElseThrow(() -> new AdminProfileNotFoundException()));
    }

    public AdminProfileDTO updateAdminProfileByAdmin(UpdateAdminProfileDTO dto) {
        AdminProfile profile = adminProfileRepository.findByUserId(dto.getUserId())
                .orElseThrow(() -> new AdminProfileNotFoundException());
        profile.setName(dto.getName());

        profile = adminProfileRepository.save(profile);
        return adminProfileMapper.toDto(profile);
    }
}
