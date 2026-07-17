package com.dapp.profileservice.api.security;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
public class HeaderAuthFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String userIdHeader = request.getHeader("x-user-id");
        String roleHeader = request.getHeader("x-user-role");

        HashMap<String, UserRole> roleMap = new HashMap<>();
        roleMap.put("ADMIN", UserRole.ROLE_ADMIN);
        roleMap.put("USER", UserRole.ROLE_USER);

        // Extract the user id.
        Long userId;
        try {
            userId = Long.parseLong(userIdHeader);
            if (userId < 0) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException e) {
            filterChain.doFilter(request, response);
            return;
        }

        // Create the set of roles.
        Set<UserRole> roles;
        if (roleHeader != null) {
            roles = Arrays.stream(roleHeader.split(",")).map((roleStr) -> roleMap.get(roleStr))
                    .filter((role) -> role != null).collect(Collectors.toSet());
        } else {
            roles = new HashSet<>();
        }

        if (!roles.isEmpty() && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails details = new HeaderUserDetails(userId, roles);
            UsernamePasswordAuthenticationToken token = new UsernamePasswordAuthenticationToken(details, null,
                    details.getAuthorities());
            token.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
            SecurityContextHolder.getContext().setAuthentication(token);

        }
        filterChain.doFilter(request, response);
    }

}
