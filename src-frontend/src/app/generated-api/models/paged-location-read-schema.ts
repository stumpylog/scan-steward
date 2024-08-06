/* tslint:disable */
/* eslint-disable */
import { LocationReadSchema } from "../models/location-read-schema";
export interface PagedLocationReadSchema {
	count: number;
	items: Array<LocationReadSchema>;
}
