package com.dapp.profileservice.common.model;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class UpdateAdminProfileDTO {
    @NotNull
    @Min(0)
    private Long userId;

    @NotNull
    private String name;
}
