/* tslint:disable */
/* eslint-disable */
export interface AlbumWithImagesReadSchema {
	/**
	 * The description of the album
	 */
	description?: string | null;

	/**
	 * The id of the album
	 */
	id: number;

	/**
	 * The ids of the images in this album in sorted order
	 */
	image_ids: Array<number>;

	/**
	 * The name of the album
	 */
	name: string;
}
