/* tslint:disable */
/* eslint-disable */
import { AlbumBasicReadSchema } from "../models/album-basic-read-schema";
export interface PagedAlbumBasicReadSchema {
	count: number;
	items: Array<AlbumBasicReadSchema>;
}
