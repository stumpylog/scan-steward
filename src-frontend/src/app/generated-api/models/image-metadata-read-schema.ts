/* tslint:disable */
/* eslint-disable */
import { RotationEnum } from "../models/rotation-enum";
export interface ImageMetadataReadSchema {
	album_ids?: Array<number> | null;
	date_id?: number | null;
	description?: string | null;
	location_id?: number | null;
	orientation: RotationEnum;
	tag_ids?: Array<number> | null;
}
