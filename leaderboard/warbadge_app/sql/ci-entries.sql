CREATE TABLE IF NOT EXISTS `ci_warbadge`.`entries` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `badge_mac` VARCHAR(45) NOT NULL,
  `ssid` VARCHAR(64) NOT NULL,
  `bssid_mac` VARCHAR(45) NOT NULL,
  `rssi` BIGINT NOT NULL,
  PRIMARY KEY (`id`));