/* tslint:disable */
/* eslint-disable */
import { RotationEnum } from "../models/rotation-enum";
export interface ImageMetadataUpdateSchema {
	date_id?: number | null;
	description?: string | null;
	location_id?: number | null;
	orientation?: RotationEnum | null;
}
