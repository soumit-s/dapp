package com.dapp.inventory.schema;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class StoreCreatedEventDto extends KafkaEventDto {
    private StoreCreatedEventPayloadDto payload;
}
