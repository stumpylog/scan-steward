import { Component } from '@angular/core';
import { IngredientModel } from '../shared/models/ingredient.model';

@Component({
  selector: 'app-shopping-list',
  templateUrl: './shopping-list.component.html',
  styleUrl: './shopping-list.component.css',
})
export class ShoppingListComponent {
  ingredients: IngredientModel[] = [
    new IngredientModel('Apples', 10),
    new IngredientModel('Tomatoes', 25),
  ];

  newItemAdded(newIngredient: IngredientModel) {
    this.ingredients.push(newIngredient);
  }
}
