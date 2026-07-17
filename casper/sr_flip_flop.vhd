library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity sr_ff is
    Port ( 
        clk : in  STD_LOGIC;
	ce : in STD_LOGIC:='1';
	s   : in  STD_LOGIC;
        r   : in  STD_LOGIC;
        q   : out STD_LOGIC
    );
end sr_ff;

architecture Behavioral of sr_ff is
    -- Internal signal to hold the state
    signal q_internal : STD_LOGIC := '0';
begin
    process(clk)
    begin
        if rising_edge(clk) then
            -- Reset priority: If 'r' is high, output is 0 regardless of 's'
--changed to set priority
            if s = '1' then
                q_internal <= '1';
            elsif r = '1' then
                q_internal <= '0';
            end if;
            -- Note: If both 'r' and 's' are '0', q_internal holds its current value implicitly.
        end if;
    end process;

    -- Assign internal state to output port
    q <= q_internal;

end Behavioral;
