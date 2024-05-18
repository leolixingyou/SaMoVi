
"use strict";

let FaultInjection_Sensor = require('./FaultInjection_Sensor.js');
let WoowaDillyStatus = require('./WoowaDillyStatus.js');
let EgoDdVehicleStatus = require('./EgoDdVehicleStatus.js');
let VehicleCollision = require('./VehicleCollision.js');
let IntersectionStatus = require('./IntersectionStatus.js');
let SyncModeSetGear = require('./SyncModeSetGear.js');
let GhostMessage = require('./GhostMessage.js');
let FaultInjection_Tire = require('./FaultInjection_Tire.js');
let GetTrafficLightStatus = require('./GetTrafficLightStatus.js');
let VehicleCollisionData = require('./VehicleCollisionData.js');
let FaultStatusInfo_Overall = require('./FaultStatusInfo_Overall.js');
let ObjectStatusExtended = require('./ObjectStatusExtended.js');
let SyncModeCmd = require('./SyncModeCmd.js');
let WaitForTick = require('./WaitForTick.js');
let MultiEgoSetting = require('./MultiEgoSetting.js');
let EgoVehicleStatusExtended = require('./EgoVehicleStatusExtended.js');
let SensorPosControl = require('./SensorPosControl.js');
let SyncModeScenarioLoad = require('./SyncModeScenarioLoad.js');
let DillyCmdResponse = require('./DillyCmdResponse.js');
let MoraiSimProcStatus = require('./MoraiSimProcStatus.js');
let MapSpecIndex = require('./MapSpecIndex.js');
let MoraiSrvResponse = require('./MoraiSrvResponse.js');
let ReplayInfo = require('./ReplayInfo.js');
let WaitForTickResponse = require('./WaitForTickResponse.js');
let SyncModeResultResponse = require('./SyncModeResultResponse.js');
let CollisionData = require('./CollisionData.js');
let SkidSteer6wUGVCtrlCmd = require('./SkidSteer6wUGVCtrlCmd.js');
let ObjectStatusList = require('./ObjectStatusList.js');
let DillyCmd = require('./DillyCmd.js');
let SyncModeInfo = require('./SyncModeInfo.js');
let FaultStatusInfo_Sensor = require('./FaultStatusInfo_Sensor.js');
let SkateboardCtrlCmd = require('./SkateboardCtrlCmd.js');
let TrafficLight = require('./TrafficLight.js');
let VehicleSpec = require('./VehicleSpec.js');
let RadarDetection = require('./RadarDetection.js');
let IntersectionControl = require('./IntersectionControl.js');
let FaultInjection_Controller = require('./FaultInjection_Controller.js');
let DdCtrlCmd = require('./DdCtrlCmd.js');
let NpcGhostCmd = require('./NpcGhostCmd.js');
let ScenarioLoad = require('./ScenarioLoad.js');
let SyncModeCtrlCmd = require('./SyncModeCtrlCmd.js');
let ObjectStatusListExtended = require('./ObjectStatusListExtended.js');
let EgoVehicleStatus = require('./EgoVehicleStatus.js');
let SkateboardStatus = require('./SkateboardStatus.js');
let CtrlCmd = require('./CtrlCmd.js');
let ERP42Info = require('./ERP42Info.js');
let PRCtrlCmd = require('./PRCtrlCmd.js');
let SetTrafficLight = require('./SetTrafficLight.js');
let SyncModeRemoveObject = require('./SyncModeRemoveObject.js');
let MoraiSimProcHandle = require('./MoraiSimProcHandle.js');
let SyncModeCmdResponse = require('./SyncModeCmdResponse.js');
let MoraiTLInfo = require('./MoraiTLInfo.js');
let FaultInjection_Response = require('./FaultInjection_Response.js');
let PREvent = require('./PREvent.js');
let MultiPlayEventRequest = require('./MultiPlayEventRequest.js');
let MoraiTLIndex = require('./MoraiTLIndex.js');
let SVADC = require('./SVADC.js');
let GPSMessage = require('./GPSMessage.js');
let SkidSteer6wUGVStatus = require('./SkidSteer6wUGVStatus.js');
let PRStatus = require('./PRStatus.js');
let RadarDetections = require('./RadarDetections.js');
let Lamps = require('./Lamps.js');
let SaveSensorData = require('./SaveSensorData.js');
let VehicleSpecIndex = require('./VehicleSpecIndex.js');
let EventInfo = require('./EventInfo.js');
let FaultStatusInfo = require('./FaultStatusInfo.js');
let FaultStatusInfo_Vehicle = require('./FaultStatusInfo_Vehicle.js');
let NpcGhostInfo = require('./NpcGhostInfo.js');
let IntscnTL = require('./IntscnTL.js');
let ObjectStatus = require('./ObjectStatus.js');
let MultiPlayEventResponse = require('./MultiPlayEventResponse.js');
let SyncModeAddObject = require('./SyncModeAddObject.js');
let MapSpec = require('./MapSpec.js');

module.exports = {
  FaultInjection_Sensor: FaultInjection_Sensor,
  WoowaDillyStatus: WoowaDillyStatus,
  EgoDdVehicleStatus: EgoDdVehicleStatus,
  VehicleCollision: VehicleCollision,
  IntersectionStatus: IntersectionStatus,
  SyncModeSetGear: SyncModeSetGear,
  GhostMessage: GhostMessage,
  FaultInjection_Tire: FaultInjection_Tire,
  GetTrafficLightStatus: GetTrafficLightStatus,
  VehicleCollisionData: VehicleCollisionData,
  FaultStatusInfo_Overall: FaultStatusInfo_Overall,
  ObjectStatusExtended: ObjectStatusExtended,
  SyncModeCmd: SyncModeCmd,
  WaitForTick: WaitForTick,
  MultiEgoSetting: MultiEgoSetting,
  EgoVehicleStatusExtended: EgoVehicleStatusExtended,
  SensorPosControl: SensorPosControl,
  SyncModeScenarioLoad: SyncModeScenarioLoad,
  DillyCmdResponse: DillyCmdResponse,
  MoraiSimProcStatus: MoraiSimProcStatus,
  MapSpecIndex: MapSpecIndex,
  MoraiSrvResponse: MoraiSrvResponse,
  ReplayInfo: ReplayInfo,
  WaitForTickResponse: WaitForTickResponse,
  SyncModeResultResponse: SyncModeResultResponse,
  CollisionData: CollisionData,
  SkidSteer6wUGVCtrlCmd: SkidSteer6wUGVCtrlCmd,
  ObjectStatusList: ObjectStatusList,
  DillyCmd: DillyCmd,
  SyncModeInfo: SyncModeInfo,
  FaultStatusInfo_Sensor: FaultStatusInfo_Sensor,
  SkateboardCtrlCmd: SkateboardCtrlCmd,
  TrafficLight: TrafficLight,
  VehicleSpec: VehicleSpec,
  RadarDetection: RadarDetection,
  IntersectionControl: IntersectionControl,
  FaultInjection_Controller: FaultInjection_Controller,
  DdCtrlCmd: DdCtrlCmd,
  NpcGhostCmd: NpcGhostCmd,
  ScenarioLoad: ScenarioLoad,
  SyncModeCtrlCmd: SyncModeCtrlCmd,
  ObjectStatusListExtended: ObjectStatusListExtended,
  EgoVehicleStatus: EgoVehicleStatus,
  SkateboardStatus: SkateboardStatus,
  CtrlCmd: CtrlCmd,
  ERP42Info: ERP42Info,
  PRCtrlCmd: PRCtrlCmd,
  SetTrafficLight: SetTrafficLight,
  SyncModeRemoveObject: SyncModeRemoveObject,
  MoraiSimProcHandle: MoraiSimProcHandle,
  SyncModeCmdResponse: SyncModeCmdResponse,
  MoraiTLInfo: MoraiTLInfo,
  FaultInjection_Response: FaultInjection_Response,
  PREvent: PREvent,
  MultiPlayEventRequest: MultiPlayEventRequest,
  MoraiTLIndex: MoraiTLIndex,
  SVADC: SVADC,
  GPSMessage: GPSMessage,
  SkidSteer6wUGVStatus: SkidSteer6wUGVStatus,
  PRStatus: PRStatus,
  RadarDetections: RadarDetections,
  Lamps: Lamps,
  SaveSensorData: SaveSensorData,
  VehicleSpecIndex: VehicleSpecIndex,
  EventInfo: EventInfo,
  FaultStatusInfo: FaultStatusInfo,
  FaultStatusInfo_Vehicle: FaultStatusInfo_Vehicle,
  NpcGhostInfo: NpcGhostInfo,
  IntscnTL: IntscnTL,
  ObjectStatus: ObjectStatus,
  MultiPlayEventResponse: MultiPlayEventResponse,
  SyncModeAddObject: SyncModeAddObject,
  MapSpec: MapSpec,
};
