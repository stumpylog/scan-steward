/* tslint:disable */
/* eslint-disable */
import { BoundingBoxSchema } from "../models/bounding-box-schema";
export interface PersonWithBoxSchema {
	/**
	 * Bounding box of the person's face
	 */
	box: BoundingBoxSchema;

	/**
	 * Person ID
	 */
	person_id: number;
}
