import { Component } from '@angular/core';
import { RecipeModel } from '../../shared/models/recipe.model';

@Component({
  selector: 'app-recipe-list',
  templateUrl: './recipe-list.component.html',
  styleUrl: './recipe-list.component.css',
})
export class RecipeListComponent {
  recipes: RecipeModel[] = [
    new RecipeModel(
      'Test Recipe',
      'this is a desc',
      'https://upload.wikimedia.org/wikipedia/commons/3/39/Recipe.jpg',
    ),
    new RecipeModel(
      'Another Recipe',
      'this is a desc',
      'https://upload.wikimedia.org/wikipedia/commons/3/39/Recipe.jpg',
    ),
  ];

  constructor() {}
}
