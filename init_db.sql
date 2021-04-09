/*
 Navicat Premium Data Transfer

 Source Server         : wx
 Source Server Type    : SQLite
 Source Server Version : 3026000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3026000
 File Encoding         : 65001

 Date: 08/04/2021 14:51:32
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS "chufang_contract";
CREATE TABLE "chufang_contract" (
  "id" INTEGER NOT NULL,
  "detail_id" VARCHAR(100),
  "city" VARCHAR(30),
  "start_date" VARCHAR(30),
  "page" VARCHAR(30),
  "_index" VARCHAR(30),
  "contract_num" VARCHAR(100),
  "department" VARCHAR(700),
  "seller" VARCHAR(700),
  "approver" VARCHAR(700),
  "business_circle" VARCHAR(700),
  "maintainer" VARCHAR(700),
  "renter" VARCHAR(700),
  "manage_state" VARCHAR(700),
  "approval" VARCHAR(700),
  "state" VARCHAR(700),
  "sign_reward_state" VARCHAR(700),
  "monthly_pay_method" VARCHAR(700),
  "income_state" VARCHAR(700),
  "business_state" VARCHAR(700),
  "sign_date" VARCHAR(70),
  "rent_start_date" VARCHAR(700),
  PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS "chufang_renter";
CREATE TABLE "chufang_renter" (
  "id" INTEGER NOT NULL,
  "detail_id" VARCHAR(100),
  "phone" VARCHAR(30),
  PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS "chufang_urgency";
CREATE TABLE "chufang_urgency" (
  "id" INTEGER NOT NULL,
  "detail_id" VARCHAR(100),
  "phone" VARCHAR(30),
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;