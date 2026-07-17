package com.dapp.inventory.schema;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
// {"aggregate_type":"store","aggregate_id":"2","event_type":"user.created","payload":{"id":2,"name":"HSR Store","description":"Store in HSR","lat":77.6366,"long":12.9125}}
@Data
@AllArgsConstructor
@NoArgsConstructor
public class StoreCreatedEventPayloadDto {
    private Long id;
    private String name;
    private String description;

    @JsonProperty("lat")
    private Double latitude;

    @JsonProperty("long")
    private Double longitude;
}
