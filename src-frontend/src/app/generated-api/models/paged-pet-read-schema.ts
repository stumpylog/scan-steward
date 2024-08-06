/* tslint:disable */
/* eslint-disable */
import { PetReadSchema } from "../models/pet-read-schema";
export interface PagedPetReadSchema {
	count: number;
	items: Array<PetReadSchema>;
}
