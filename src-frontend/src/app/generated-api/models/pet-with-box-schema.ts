/* tslint:disable */
/* eslint-disable */
import { BoundingBoxSchema } from "../models/bounding-box-schema";
export interface PetWithBoxSchema {
	/**
	 * Bounding box of the pet
	 */
	box: BoundingBoxSchema;

	/**
	 * Pet ID
	 */
	pet_id: number;
}
