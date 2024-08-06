import { Component } from "@angular/core";
import { NgbActiveModal } from "@ng-bootstrap/ng-bootstrap";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { PeopleService } from "../../generated-api/services";
import { finalize, tap } from "rxjs/operators";

@Component({
	selector: "app-personcreate",
	templateUrl: "./person-create.component.html",
	styleUrl: "./person-create.component.css",
})
export class PersonCreateComponent {
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

	onSubmit() {
		if (this.personForm.valid) {
			this.isLoading = true;
			console.log(this.personForm.value);
			this.peopleService
				.createPerson({ body: this.personForm.value })
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
						console.error("Error creating person:", error);
						this.activeModal.dismiss("Error creating person");
					},
				});
		}
	}
}
