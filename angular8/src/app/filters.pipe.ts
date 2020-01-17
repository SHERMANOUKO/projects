import { Pipe, PipeTransform } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Pipe({
  name: 'filters'
})
export class FiltersPipe implements PipeTransform {

  transform(values: Observable<any[]>, searchText: any): any {
    if(!values) return []
    if(!searchText) return []
    return values.pipe(
      map<any, any>(data => data.filter(x => x.propertystartingPrice <= searchText.price))
    );
  }

  

  // import { Pipe, PipeTransform } from '@angular/core';
  // @Pipe({
  //   name: 'filter'
  // })
  // export class FilterPipe implements PipeTransform {
  //   transform(items: any[], searchText: string): any[] {
  //     if(!items) return [];
  //     if(!searchText) return items;
      
  //     searchText = searchText.toLowerCase();
  //         return items.filter( it => {
  //           return it.name.toLowerCase().includes(searchText);
  //         });
  //   } 
  // }
}
