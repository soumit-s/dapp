package com.dapp.profileservice.kafka_listener.model;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class UserCreatedEventDTO extends EventDTO {

    @NotNull
    UserCreatedPayloadDTO payload;
}
