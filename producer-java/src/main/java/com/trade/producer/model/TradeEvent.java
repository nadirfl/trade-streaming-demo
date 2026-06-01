package com.trade.producer.model;

import java.math.BigDecimal;
import java.time.Instant;

public record TradeEvent(
    String eventId,
    String tradeId,
    String eventType,
    Instant eventTimestamp,
    BigDecimal quantity,
    BigDecimal price,
    String counterparty,
    String instrument,
    String currency
) {
}