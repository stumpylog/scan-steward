import { Component, Input } from "@angular/core";
import { NgbActiveModal } from "@ng-bootstrap/ng-bootstrap";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";

import { PeopleService } from "../../generated-api/services";
import { PersonReadSchema } from "../../generated-api/models";
import { finalize, tap } from "rxjs/operators";

@Component({
	selector: "app-person-edit",
	templateUrl: "./person-edit.component.html",
	styleUrl: "./person-edit.component.css",
})
export class PersonEditComponent {
	@Input() public person!: PersonReadSchema;
	personForm: FormGroup;
	isLoading = false;

	constructor(
		public activeModal: NgbActiveModal,
		private formBuilder: FormBuilder,
		private peopleService: PeopleService,
	) {
		this.personForm = this.formBuilder.group({
			name: ["", Validators.required],
			description: [""],
		});
	}

	ngOnInit() {
		this.personForm.patchValue({
			name: this.person.name,
			description: this.person.description,
		});
	}

	onSubmit() {
		if (this.personForm.valid) {
			this.isLoading = true;
			this.peopleService
				.updatePerson({
					person_id: this.person.id,
					body: this.personForm.value,
				})
				.pipe(
					tap(() => {
						this.activeModal.close("Save click");
					}),
					finalize(() => {
						this.isLoading = false;
					}),
				)
				.subscribe({
					error: (error) => {
						console.error("Error updating person:", error);
						this.activeModal.dismiss("Error updating person");
					},
				});
		}
	}
}
