package com.dapp.profileservice.api.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;

import com.dapp.profileservice.api.model.UpdateAdminProfileByAdminRequestDTO;
import com.dapp.profileservice.api.security.HeaderUserId;
import com.dapp.profileservice.common.model.AdminProfileDTO;
import com.dapp.profileservice.common.model.UpdateAdminProfileDTO;
import com.dapp.profileservice.common.service.ProfileService;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
@RequestMapping("/api/v1/admin")
public class AdminController {
    private final ProfileService profileService;

    public AdminController(ProfileService profileService) {
        this.profileService = profileService;
    }

    @GetMapping("profile")
    public ResponseEntity<AdminProfileDTO> getProfile(@HeaderUserId Long userId) {
        return ResponseEntity.ok(profileService.getAdminProfileByUserId(userId));
    }

    @PutMapping("profile")
    public ResponseEntity<AdminProfileDTO> updateProfile(@HeaderUserId Long userId,
            @RequestBody UpdateAdminProfileByAdminRequestDTO body) {
        UpdateAdminProfileDTO dto = new UpdateAdminProfileDTO();
        dto.setName(body.getName());
        dto.setUserId(userId);

        AdminProfileDTO profile = profileService.updateAdminProfileByAdmin(dto);
        return ResponseEntity.ok(profile);
    }

}
