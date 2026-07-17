package com.dapp.inventory.schema;

import lombok.Data;
import lombok.NoArgsConstructor;
// {
// 	"aggregate_type": "product",
// 	"aggregate_id": 1,
// 	"event_type": "product.created",
// 	"payload": {
// 		"id": 1,
// 		"name": "Fantastic Cotton Chips",
// 		"description": "Introducing the Qatar-inspired Chips, blending possible style with local craftsmanship"
// 	}
// }
@Data
@NoArgsConstructor
public class ProductCreatedEventPayloadDto {
    private Long id;
    private String name;
    private String description;
}
