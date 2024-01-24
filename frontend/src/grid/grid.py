# grid/grid.py : frontend : Fall '23 CS3300 Team 10
# This script is the grid class for the frontend.
# This is where the grid class will be defined.

import pygame as pg
import ast 
import settings as s

class Grid():

    def __init__(self, screen):
        
        self.screen = screen

        self.size = min(s.WINDOW_HEIGHT // (s.GRID_ROWS + 3), s.WINDOW_WIDTH // (s.GRID_COLS + 2))
        self.grid = pg.Surface((self.size * s.GRID_COLS, self.size * s.GRID_ROWS))
        self.grid_rect = pg.Rect(s.WINDOW_WIDTH // 2 - self.grid.get_width() // 2, 
                                ((s.WINDOW_HEIGHT - self.grid.get_height()) - self.size), 
                                self.grid.get_width(), self.grid.get_height())

        self.cells = {}
        self.new_cells = {}
        self.selected_cell = None

    def event_handler(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:
            
            if self.grid_rect.collidepoint(event.pos):

                selected_cell_x = (event.pos[0] - self.grid_rect.x) // self.size
                selected_cell_y = (event.pos[1] - self.grid_rect.y) // self.size
                key = f'{selected_cell_x},{selected_cell_y}'

                # If left mouse button is clicked and the cell is not in the cells dict, 
                # insert cell into new_cells dict
                if event.button == 1 and key not in self.cells:
                    self.new_cells[key] = ('1', pg.Rect(selected_cell_x * self.size, 
                                                        selected_cell_y * self.size, 
                                                        self.size, self.size))
                    self.selected_cell = self.new_cells[key][1]

                elif event.button == 3:
                    if key in self.new_cells:
                        del self.new_cells[key]

    def draw(self):

        self.grid.fill(s.WHITE)

        # Draw every cell in cells dict
        for cell in self.cells.values():
            pg.draw.rect(self.grid, s.COLORS[str(cell[0])], cell[1])

        # Draw every cell in new_cells dict
        for cell in self.new_cells:
            pg.draw.rect(self.grid, s.GREY, self.new_cells[cell][1])

        # Horizontal lines
        for i in range(s.GRID_ROWS + 1):
            pg.draw.line(self.grid, s.GREY, (0, i * self.size), (s.GRID_COLS * self.size, i * self.size), 2)

        # Vertical lines
        for i in range(s.GRID_COLS + 1):
            pg.draw.line(self.grid, s.GREY, (i * self.size, 0), (i * self.size, s.GRID_ROWS * self.size), 2)

        # Draw grid surface on screen
        self.screen.blit(self.grid, (s.WINDOW_WIDTH // 2 - self.grid.get_width() // 2, 
                                     (s.WINDOW_HEIGHT - self.grid.get_height()) - self.size))

        # Draw grid border
        pg.draw.rect(self.screen, s.BLACK, (s.WINDOW_WIDTH // 2 - self.grid.get_width() // 2, 
                                            ((s.WINDOW_HEIGHT - self.grid.get_height()) - self.size), 
                                            self.grid.get_width(), self.grid.get_height()), 2)


        # Draw Debug Info: Grid Size (rows x cols), Cell Size, Selected Cell (row x col), Build Version
        selected_x = self.selected_cell.x // self.size + 1 if self.selected_cell != None else 'x'
        selected_y = self.selected_cell.y // self.size + 1 if self.selected_cell != None else 'y'

        debug_info_grid_size_t = f'Grid Size: {s.GRID_ROWS} x {s.GRID_COLS}'
        debug_info_cell_size_t = f'Cell Size: {self.size}'
        debug_info_selected_cell_t = f'Selected Cell: ({selected_x}, {selected_y})'
        debug_info_build_version_t = f'Build Version: {s.BUILD_VERSION}'

        font = pg.font.Font(None, 24)
        debug_info_grid_size = font.render(debug_info_grid_size_t, True, s.GREEN)
        debug_info_cell_size = font.render(debug_info_cell_size_t, True, s.GREEN)
        debug_info_selected_cell = font.render(debug_info_selected_cell_t, True, s.GREEN)
        debug_info_build_version = font.render(debug_info_build_version_t, True, s.GREEN)

        # Blit debug info to screen
        if s.DEBUG:
            self.screen.blit(debug_info_build_version, (10, 10))
            self.screen.blit(debug_info_grid_size, (10, 30))
            self.screen.blit(debug_info_cell_size, (10, 50))
            self.screen.blit(debug_info_selected_cell, (10, 70))
            
    def update(self, grid_str):
        cell_list = ast.literal_eval(grid_str)
        self.cells = {}
        
        for row_idx, row in enumerate(cell_list):
            for col_idx, col in enumerate(row):
                key = f'{row_idx},{col_idx}'
                if col != 0:    
                    self.cells[key] = (col, pg.Rect(row_idx * self.size, col_idx * self.size, self.size, self.size))
                    
        self.selected_cell = None
        self.new_cells = dict()

    def get_cells(self):
        return self.cells
    
    def get_new_cells_str(self):
        
        ret = ''

        for cell in self.new_cells:
            ret += f'({cell}),'

        return ret
