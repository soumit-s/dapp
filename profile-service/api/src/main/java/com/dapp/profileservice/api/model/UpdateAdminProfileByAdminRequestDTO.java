package com.dapp.profileservice.api.model;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class UpdateAdminProfileByAdminRequestDTO {
    @NotNull
    @Size(min = 1)
    private String name;
}
