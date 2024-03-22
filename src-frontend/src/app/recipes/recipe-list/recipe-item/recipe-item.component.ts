import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RecipeModel } from '../../../shared/models/recipe.model';

@Component({
  selector: 'app-recipe-item',
  templateUrl: './recipe-item.component.html',
  styleUrl: './recipe-item.component.css',
})
export class RecipeItemComponent {
  @Input() inputRecipe: RecipeModel;
  @Output() detailEvent = new EventEmitter<void>();

  onDetailView(event: string) {
    this.detailEvent.emit();
  }
}
