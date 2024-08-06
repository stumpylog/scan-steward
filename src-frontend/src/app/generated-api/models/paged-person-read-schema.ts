/* tslint:disable */
/* eslint-disable */
import { PersonReadSchema } from "../models/person-read-schema";
export interface PagedPersonReadSchema {
	count: number;
	items: Array<PersonReadSchema>;
}
