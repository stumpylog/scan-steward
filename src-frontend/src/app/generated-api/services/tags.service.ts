/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { createTag } from "../fn/tags/create-tag";
import { CreateTag$Params } from "../fn/tags/create-tag";
import { deleteTag } from "../fn/tags/delete-tag";
import { DeleteTag$Params } from "../fn/tags/delete-tag";
import { getAllTags } from "../fn/tags/get-all-tags";
import { GetAllTags$Params } from "../fn/tags/get-all-tags";
import { getSingleTag } from "../fn/tags/get-single-tag";
import { GetSingleTag$Params } from "../fn/tags/get-single-tag";
import { getTagTree } from "../fn/tags/get-tag-tree";
import { GetTagTree$Params } from "../fn/tags/get-tag-tree";
import { PagedTagRead } from "../models/paged-tag-read";
import { TagRead } from "../models/tag-read";
import { TagTree } from "../models/tag-tree";
import { updateTag } from "../fn/tags/update-tag";
import { UpdateTag$Params } from "../fn/tags/update-tag";

@Injectable({ providedIn: "root" })
export class TagsService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getTagTree()` */
	static readonly GetTagTreePath = "/api/tag/tree/";

	/**
	 * Get Tag Tree.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getTagTree()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getTagTree$Response(
		params?: GetTagTree$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<TagTree>>> {
		return getTagTree(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Tag Tree.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getTagTree$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getTagTree(
		params?: GetTagTree$Params,
		context?: HttpContext,
	): Observable<Array<TagTree>> {
		return this.getTagTree$Response(params, context).pipe(
			map((r: StrictHttpResponse<Array<TagTree>>): Array<TagTree> => r.body),
		);
	}

	/** Path part for operation `getAllTags()` */
	static readonly GetAllTagsPath = "/api/tag/";

	/**
	 * Get Tags.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getAllTags()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getAllTags$Response(
		params?: GetAllTags$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PagedTagRead>> {
		return getAllTags(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Tags.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getAllTags$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getAllTags(
		params?: GetAllTags$Params,
		context?: HttpContext,
	): Observable<PagedTagRead> {
		return this.getAllTags$Response(params, context).pipe(
			map((r: StrictHttpResponse<PagedTagRead>): PagedTagRead => r.body),
		);
	}

	/** Path part for operation `createTag()` */
	static readonly CreateTagPath = "/api/tag/";

	/**
	 * Create Tag.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `createTag()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createTag$Response(
		params: CreateTag$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<TagRead>> {
		return createTag(this.http, this.rootUrl, params, context);
	}

	/**
	 * Create Tag.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `createTag$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createTag(
		params: CreateTag$Params,
		context?: HttpContext,
	): Observable<TagRead> {
		return this.createTag$Response(params, context).pipe(
			map((r: StrictHttpResponse<TagRead>): TagRead => r.body),
		);
	}

	/** Path part for operation `getSingleTag()` */
	static readonly GetSingleTagPath = "/api/tag/{tag_id}/";

	/**
	 * Get Single Tag.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getSingleTag()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSingleTag$Response(
		params: GetSingleTag$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<TagRead>> {
		return getSingleTag(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Single Tag.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getSingleTag$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSingleTag(
		params: GetSingleTag$Params,
		context?: HttpContext,
	): Observable<TagRead> {
		return this.getSingleTag$Response(params, context).pipe(
			map((r: StrictHttpResponse<TagRead>): TagRead => r.body),
		);
	}

	/** Path part for operation `deleteTag()` */
	static readonly DeleteTagPath = "/api/tag/{tag_id}/";

	/**
	 * Delete Tag.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deleteTag()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteTag$Response(
		params: DeleteTag$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<void>> {
		return deleteTag(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Tag.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deleteTag$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteTag(params: DeleteTag$Params, context?: HttpContext): Observable<void> {
		return this.deleteTag$Response(params, context).pipe(
			map((r: StrictHttpResponse<void>): void => r.body),
		);
	}

	/** Path part for operation `updateTag()` */
	static readonly UpdateTagPath = "/api/tag/{tag_id}/";

	/**
	 * Update Tag.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateTag()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateTag$Response(
		params: UpdateTag$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<TagRead>> {
		return updateTag(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Tag.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateTag$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateTag(
		params: UpdateTag$Params,
		context?: HttpContext,
	): Observable<TagRead> {
		return this.updateTag$Response(params, context).pipe(
			map((r: StrictHttpResponse<TagRead>): TagRead => r.body),
		);
	}
}
