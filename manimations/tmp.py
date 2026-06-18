import manim as mn
from manim import *


class DatabaseTables(Scene):
    def construct(self):
        # Define data for customers table
        customers_data = [
            ["Customer#", "FirstName", "LastName"],
            ["1001", "Bonita", "Morales"],
            ["1007", "Tammy", "Giana"],
            ["1004", "Thomas", "Pierson"],
        ]
        
        # Define data for orders table
        orders_data = [
            ["Order#", "Customer#", "ShipCost"],
            ["1007", "1007", "4"],
            ["1003", "1001", "5"],
            ["1008", "1004", "3"],
            ["1018", "1001", "3"],
            ["1014", "1007", "8"],
        ]
        
        # Define data for results table (INNER JOIN of customers and orders)
        results_data = [
            ["Customer#", "FirstName", "LastName", "Order#", "Customer#", "ShipCost"],
            ["1001", "Bonita", "Morales", "1003", "1001", "5"],
            ["1001", "Bonita", "Morales", "1018", "1001", "3"],
            ["1004", "Thomas", "Pierson", "1008", "1004", "3"],
            ["1007", "Tammy", "Giana", "1007", "1007", "4"],
            ["1007", "Tammy", "Giana", "1014", "1007", "8"]
        ]
        
        # Create customers table
        customers_table = Table(
            customers_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2, "color": WHITE},
            element_to_mobject=Text,
            element_to_mobject_config={"color": WHITE}
        )
        customers_table.scale(0.4)
        
        # Create orders table
        orders_table = Table(
            orders_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2, "color": WHITE},
            element_to_mobject=Text,
            element_to_mobject_config={"color": WHITE}
        )
        orders_table.scale(0.4)
        
        # Position tables
        customers_table.to_edge(LEFT, buff=0.5)
        orders_table.to_edge(RIGHT, buff=0.5)
        
        # Add titles
        customers_title = Text("Customers Table").scale(0.6).next_to(customers_table, UP)
        orders_title = Text("Orders Table").scale(0.6).next_to(orders_table, UP)
        
        # Animate the tables and titles
        self.play(
            Create(customers_table),
            Create(orders_table),
            Write(customers_title),
            Write(orders_title)
        )
        
        # Create arrows from Customer ID to Order CustomerID
        arrows = []
        # Map Customer IDs to their table cell indices (row, col)
        customer_ids = {
            "1001": customers_table.get_entries((2, 1)),  # Customer# 1001
            "1007": customers_table.get_entries((3, 1)),  # Customer# 1007
            "1004": customers_table.get_entries((4, 1)),  # Customer# 1004
        }
        # Map Order CustomerIDs to their table cell indices and customer IDs
        order_customer_ids = [
            (orders_table.get_entries((2, 2)), "1007"),  # Order 1007, Customer# 1007
            (orders_table.get_entries((3, 2)), "1001"),  # Order 1003, Customer# 1001
            (orders_table.get_entries((4, 2)), "1004"),  # Order 1008, Customer# 1004
            (orders_table.get_entries((5, 2)), "1001"),  # Order 1018, Customer# 1001
            (orders_table.get_entries((6, 2)), "1007"),  # Order 1014, Customer# 1007
        ]
        
        # Define colors for different customers (used for arrows)
        color_map = {
            "1001": BLUE,   # Customer# 1001 (Bonita)
            "1007": RED,    # Customer# 1007 (Tammy)
            "1004": GREEN   # Customer# 1004 (Thomas)
        }
        
        # Create arrows with different colors
        for order_cell, cust_id in order_customer_ids:
            if cust_id in customer_ids:
                arrow = Arrow(
                    start=customer_ids[cust_id].get_center(),
                    end=order_cell.get_center(),
                    color=color_map[cust_id],
                    stroke_width=3,
                    buff=0.1
                )
                arrows.append(arrow)
        
        # Animate the arrows slowly, one by one
        for arrow in arrows:
            self.play(Create(arrow, run_time=2))
        
        # Remove the arrows
        self.play(*[FadeOut(arrow) for arrow in arrows])
        
        # Group tables with their titles for moving
        customers_group = VGroup(customers_table, customers_title)
        orders_group = VGroup(orders_table, orders_title)
        
        # Shrink and move tables to upper left and upper right corners
        self.play(
            customers_group.animate.scale(0.3 / 0.4).to_corner(UL, buff=0.5),
            orders_group.animate.scale(0.3 / 0.4).to_corner(UR, buff=0.5)
        )
        
        # Create results table
        results_table = Table(
            results_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2, "color": WHITE},
            element_to_mobject=Text,
            element_to_mobject_config={"color": WHITE}
        )
        results_table.scale(0.4)
        results_table.to_corner(DL, buff=0.5)
        
        # Add results table title
        results_title = Text("Results Table (Customers INNER JOIN Orders)").scale(0.6).next_to(results_table, UP)
        
        # Animate the results table header
        header_row = results_table.get_rows()[0]
        self.play(
            Create(header_row),
            Write(results_title)
        )
        
        # Map results table rows to corresponding customers and orders rows
        row_mappings = [
            (2, 2, 3, "1001"),  # Results row 1: Customer# 1001 (row 2), Order# 1003 (row 3)
            (3, 2, 5, "1001"),  # Results row 2: Customer# 1001 (row 2), Order# 1018 (row 5)
            (4, 4, 4, "1004"),  # Results row 3: Customer# 1004 (row 4), Order# 1008 (row 4)
            (5, 3, 2, "1007"),  # Results row 4: Customer# 1007 (row 3), Order# 1007 (row 2)
            (6, 3, 6, "1007"),  # Results row 5: Customer# 1007 (row 3), Order# 1014 (row 6)
        ]
        
        # Animate each results table row with highlights and copying
        for result_row_idx, customer_row_idx, order_row_idx, cust_id in row_mappings:
            # Get the rows to highlight
            customer_row = customers_table.get_rows()[customer_row_idx - 1]
            order_row = orders_table.get_rows()[order_row_idx - 1]
            result_row = results_table.get_rows()[result_row_idx - 1]
            
            # Create highlight rectangles
            customer_highlight = BackgroundRectangle(customer_row, fill_color=YELLOW, fill_opacity=0.3)
            order_highlight = BackgroundRectangle(order_row, fill_color=PURPLE, fill_opacity=0.3)
            
            # Animate highlights
            self.play(
                FadeIn(customer_highlight),
                FadeIn(order_highlight),
                run_time=1
            )
            self.wait(0.5)
            
            # Create copies of relevant entries
            customer_entries = [
                customers_table.get_entries((customer_row_idx, 1)),  # Customer#
                customers_table.get_entries((customer_row_idx, 2)),  # FirstName
                customers_table.get_entries((customer_row_idx, 3)),  # LastName
            ]
            order_entries = [
                orders_table.get_entries((order_row_idx, 1)),  # Order#
                orders_table.get_entries((order_row_idx, 2)),  # Customer#
                orders_table.get_entries((order_row_idx, 3)),  # ShipCost
            ]
            
            # Create Text objects for copies with matching highlight colors
            customer_copies = [Text(entry.text, color=YELLOW).move_to(entry.get_center()).scale(0.4 * 0.3 / 0.4) for entry in customer_entries]
            order_copies = [Text(entry.text, color=PURPLE).move_to(entry.get_center()).scale(0.4 * 0.3 / 0.4) for entry in order_entries]
            
            # Define target positions in results table (maintaining column order)
            result_positions = [
                results_table.get_entries((result_row_idx, 1)).get_center(),  # Customer# (from Customers)
                results_table.get_entries((result_row_idx, 2)).get_center(),  # FirstName (from customers)
                results_table.get_entries((result_row_idx, 3)).get_center(),  # LastName (from customers)
                results_table.get_entries((result_row_idx, 4)).get_center(),  # Order# (from orders)
                results_table.get_entries((result_row_idx, 5)).get_center(),  # Customer# (from orders)
                results_table.get_entries((result_row_idx, 6)).get_center(),  # ShipCost (from orders)
            ]
            
            # Animate copying (maintaining column order)
            self.play(
                *[Transform(copy, copy.copy().move_to(pos)) for copy, pos in zip(
                    [customer_copies[0], customer_copies[1], customer_copies[2], order_copies[0], order_copies[1], order_copies[2]],
                    result_positions
                )],
                run_time=2
            )
            self.wait(1.0)
            
            # Fade out copies and create the actual results row
            self.play(
                *[FadeOut(copy) for copy in order_copies + customer_copies],
                Create(result_row),
                run_time=2
            )
            
            # Remove highlights
            self.play(
                FadeOut(customer_highlight),
                FadeOut(order_highlight),
                run_time=2
            )
        
        self.wait(5)