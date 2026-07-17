package com.dapp.profileservice.common.mapper;

import org.mapstruct.Mapper;

import com.dapp.profileservice.common.entity.AdminProfile;
import com.dapp.profileservice.common.model.AdminProfileDTO;
import com.dapp.profileservice.common.model.CreateAdminProfileDTO;

@Mapper(componentModel = "spring")
public interface AdminProfileMapper {
    AdminProfileDTO toDto(AdminProfile entity);

    AdminProfile toEntity(AdminProfileDTO dto);
    AdminProfile toEntity(CreateAdminProfileDTO dto);
}
