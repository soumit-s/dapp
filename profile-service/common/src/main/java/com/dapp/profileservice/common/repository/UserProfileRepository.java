package com.dapp.profileservice.common.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.dapp.profileservice.common.entity.UserProfile;

public interface UserProfileRepository extends JpaRepository<UserProfile, Long> {
    
}
