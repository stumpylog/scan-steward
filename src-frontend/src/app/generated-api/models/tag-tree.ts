/* tslint:disable */
/* eslint-disable */
export interface TagTree {
	applied: boolean;
	children?: Array<TagTree> | null;
	description?: string | null;
	id: number;
	name: string;
	parent_id?: number | null;
}
