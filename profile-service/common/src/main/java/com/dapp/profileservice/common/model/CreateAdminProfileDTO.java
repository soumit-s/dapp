package com.dapp.profileservice.common.model;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class CreateAdminProfileDTO {
    @NotNull
    @Min(0)
    private Long userId;

    @NotNull
    private String name;

    @Email
    @NotNull
    private String email;
}
