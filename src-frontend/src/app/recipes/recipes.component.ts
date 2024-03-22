import { Component } from '@angular/core';
import { RecipeModel } from '../shared/models/recipe.model';

@Component({
  selector: 'app-recipes',
  templateUrl: './recipes.component.html',
  styleUrl: './recipes.component.css',
})
export class RecipesComponent {
  selectedRecipe: RecipeModel;

  recipeSelected(recipe: RecipeModel) {
    this.selectedRecipe = recipe;
  }
}
