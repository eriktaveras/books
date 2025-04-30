import pandas as pd
import re
from django.core.management.base import BaseCommand
from libros.models import Book, DeweyCode

class Command(BaseCommand):
    help = 'Import books from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='data/BCF.csv',
                            help='CSV file with books data')
        parser.add_argument('--encoding', type=str, default='latin1',
                            help='File encoding (default: latin1)')
        parser.add_argument('--limit', type=int, default=0,
                            help='Limit the number of books to import (0 for all)')

    def handle(self, *args, **options):
        file_path = options['file']
        encoding = options['encoding']
        limit = options['limit']
        
        self.stdout.write(self.style.SUCCESS(f'Reading from {file_path} with encoding {encoding}'))
        
        try:
            # Read the CSV file
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Limit rows if specified
            if limit > 0:
                df = df.head(limit)
                self.stdout.write(self.style.WARNING(f'Limiting import to {limit} books'))
            
            # Count before import
            count_before = Book.objects.count()
            
            # Import data
            books_created = 0
            books_updated = 0
            dewey_missing = 0
            
            # Get all Dewey codes from database for faster lookup
            all_dewey_codes = {code.code: code for code in DeweyCode.objects.all()}
            self.stdout.write(self.style.SUCCESS(f'Loaded {len(all_dewey_codes)} Dewey codes from database'))
            
            for _, row in df.iterrows():
                try:
                    title = str(row.get('title', '')).strip()
                    if not title or title == 'nan':
                        continue
                    
                    # Extract data from row
                    author = str(row.get('author', '')).strip() if not pd.isna(row.get('author')) else ''
                    
                    # Handle publication year - might be in various formats
                    pub_year = None
                    if not pd.isna(row.get('year')):
                        year_str = str(row.get('year')).strip()
                        # Try to extract a 4-digit year
                        year_match = re.search(r'\b(19|20)\d{2}\b', year_str)
                        if year_match:
                            pub_year = int(year_match.group())
                        elif year_str.isdigit() and len(year_str) == 4:
                            pub_year = int(year_str)
                    
                    publisher = str(row.get('editorial', '')).strip() if not pd.isna(row.get('editorial')) else ''
                    
                    # Get location and status
                    location = str(row.get('location', '')).strip() if not pd.isna(row.get('location')) else ''
                    status = 'Available'  # Default status
                    
                    # Handle ISBN - it might be in observations or other fields
                    isbn = ''
                    
                    # Handle Dewey code - extract from the code format like "C001.2 A832l"
                    dewey_code_obj = None
                    if not pd.isna(row.get('code')):
                        full_code = str(row.get('code')).strip()
                        if full_code and full_code != 'nan':
                            # Extract Dewey code part (e.g. 001.2 from C001.2 A832l)
                            dewey_match = re.search(r'[C]?(\d+\.\d+)', full_code)
                            if dewey_match:
                                dewey_code = dewey_match.group(1)
                                # Try different formats (e.g. 1.0 vs 001.0)
                                possible_codes = [
                                    dewey_code,
                                    dewey_code.lstrip('0'),
                                    float(dewey_code) if dewey_code.replace('.', '').isdigit() else None
                                ]
                                
                                # Try each possible format
                                for code in possible_codes:
                                    if code is not None:
                                        code_str = str(code)
                                        if code_str in all_dewey_codes:
                                            dewey_code_obj = all_dewey_codes[code_str]
                                            break
                                
                                if dewey_code_obj is None:
                                    dewey_missing += 1
                                    # Debug info
                                    if dewey_missing <= 5:  # Only show first 5 to avoid spam
                                        self.stdout.write(self.style.WARNING(
                                            f"Code not found: '{full_code}' extracted as '{dewey_code}'"
                                        ))
                    
                    # Create or update book
                    book_data = {
                        'author': author,
                        'publication_year': pub_year,
                        'publisher': publisher,
                        'location': location,
                        'status': status,
                        'dewey_code': dewey_code_obj,
                        'isbn': isbn
                    }
                    
                    book, created = Book.objects.update_or_create(
                        title=title,
                        defaults=book_data
                    )
                    
                    if created:
                        books_created += 1
                    else:
                        books_updated += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error importing book: {str(e)}'))
            
            # Count after import
            count_after = Book.objects.count()
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported books. Created: {books_created}, Updated: {books_updated}, '
                f'Total: {count_after} (Before: {count_before})'
            ))
            
            if dewey_missing > 0:
                self.stdout.write(self.style.WARNING(
                    f'Warning: {dewey_missing} books had Dewey codes that were not found in the database. '
                    f'Run import_dewey command first to import all codes.'
                ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing books: {str(e)}')) 