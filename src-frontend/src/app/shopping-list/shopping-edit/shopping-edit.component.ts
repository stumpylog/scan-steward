import { Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { IngredientModel } from '../../shared/models/ingredient.model';

@Component({
  selector: 'app-shopping-edit',
  templateUrl: './shopping-edit.component.html',
  styleUrl: './shopping-edit.component.css',
})
export class ShoppingEditComponent {
  @Output() newItemAdded = new EventEmitter<IngredientModel>();
  @ViewChild('nameInput') nameInputRef: ElementRef;
  @ViewChild('amountInput') amountInputRef: ElementRef;

  constructor() {}

  addIngredient() {
    this.newItemAdded.emit(
      new IngredientModel(
        this.nameInputRef.nativeElement.value,
        this.amountInputRef.nativeElement.value,
      ),
    );
  }
}
