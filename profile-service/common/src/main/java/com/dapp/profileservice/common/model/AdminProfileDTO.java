package com.dapp.profileservice.common.model;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AdminProfileDTO {

    @NotNull
    @Min(0)
    private Long userId;

    @Email
    @NotNull
    private String email;

    @NotNull
    private String name;
}
