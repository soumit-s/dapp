package com.dapp.profileservice.kafka_listener.model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonSetter;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import static java.util.Map.entry;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserCreatedPayloadDTO {
    private final Map<String, UserRole> strToRoleMap = Map.ofEntries(entry("ADMIN", UserRole.ROLE_ADMIN), entry("USER", UserRole.ROLE_USER));
    private final Map<UserRole, String> roleToStrMap = Map.ofEntries(entry(UserRole.ROLE_ADMIN, "ADMIN"), entry(UserRole.ROLE_USER, "USER"));

    @NotNull
    @Min(0)
    private Long id;

    private String phone;

    private String email;

    @NotNull
    @Builder.Default
    private Set<UserRole> role = new HashSet<>();
    @JsonSetter("role")
    public void setRoleFromString(List<String> roles) {
        if (roles == null) {
            return;
        }
        this.role = roles.stream().map((r) -> strToRoleMap.get(r)).filter(r -> r != null).collect(Collectors.toSet());
    }

    @JsonGetter("role")
    public List<String> getRoleAsString() {
        return role.stream().map((r) -> roleToStrMap.get(r)).toList();
    }
}
