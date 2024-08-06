import { Component, OnInit } from "@angular/core";
import { PeopleService } from "../../generated-api/services";
import { ActivatedRoute } from "@angular/router";
import { PagedPersonReadSchema } from "../../generated-api/models";
import { PersonUpdateSchema } from "../../generated-api/models";
import { catchError, throwError } from "rxjs";
import { NgbPaginationConfig } from "@ng-bootstrap/ng-bootstrap";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { PersonCreateComponent } from "../person-create/person-create.component";
import { PersonEditComponent } from "../person-edit/person-edit.component";

@Component({
	selector: "app-peoplelist",
	templateUrl: "./people-list.component.html",
	styleUrl: "./people-list.component.css",
})
export class PeopleListComponent implements OnInit {
	pagedPersons: PagedPersonReadSchema | null = null;
	page = 1;
	pageSize = 9;
	error: string | null = null;

	constructor(
		private peopleService: PeopleService,
		private paginationConfig: NgbPaginationConfig,
		private route: ActivatedRoute,
		private modalService: NgbModal,
	) {
		this.paginationConfig.maxSize = 5;
		this.paginationConfig.boundaryLinks = true;
	}

	ngOnInit() {
		this.route.queryParams.subscribe((params) => {
			this.page = params["page"] ? +params["page"] : 1;
			this.loadPage(this.page);
		});
	}

	loadPage(pageNumber: number) {
		this.peopleService
			.getPeople$Response({
				page: pageNumber,
			})
			.pipe(
				catchError((error) => {
					this.error =
						"An error occurred while fetching the people data. Please try again later.";
					return throwError(() => error);
				}),
			)
			.subscribe((response) => {
				this.pagedPersons = response.body;
				this.error = null;
			});
	}

	openCreateModal() {
		const modalRef = this.modalService.open(PersonCreateComponent, {
			ariaLabelledBy: "modal-basic-title",
			centered: true,
		});
		modalRef.result.then(
			(result) => {
				// Handle successful creation of a new person
				this.loadPage(this.page);
			},
			(reason) => {
				// Handle modal dismissal
			},
		);
	}

	openEditModal(person: PersonUpdateSchema) {
		const modalRef = this.modalService.open(PersonEditComponent, {
			ariaLabelledBy: "modal-basic-title",
			centered: true,
		});
		modalRef.componentInstance.person = person;
		modalRef.result.then(
			(result) => {
				// Handle successful update of a person
				this.loadPage(this.page);
			},
			(reason) => {
				// Handle modal dismissal
			},
		);
	}

	deletePerson(personId: number) {
		this.peopleService.deletePerson({ person_id: personId }).subscribe(
			() => {
				// Handle successful deletion of a person
				this.loadPage(this.page);
			},
			(error) => {
				console.error("Error deleting person:", error);
			},
		);
	}
}
