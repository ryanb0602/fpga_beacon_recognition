library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity small_ram_block is
    generic(
        DEPTH:INTEGER:=64;
        SSR:INTEGER:=16;
        DATA_WIDTH:INTEGER:=18;
        ADDR_WIDTH:INTEGER:=6
        )
    port(
        clk:in STD_LOGIC;
        ce:in STD_LOGIC:='1';

        vi:in STD_LOGIC;
        di:in STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0);
        addr_in:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);

        rd_addr:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        dout:out STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0)
        )
end small_ram_block;

architecture Behavioral of small_ram_block is 

    constant total_width : integer := SSR * DATA_WIDTH;
    type ram_type is array (0 to DEPTH-1) of STD_LOGIC_VECTOR(total_width-1 downto 0);
    signal ram_memory : ram_type := (others => (others => '0'));

    attribute ram_style : string;
    attribute ram_style of ram_memory : signal is "block";

begin

    process(clk)
    begin
        if rising_edge(clk) then
            if vi = '1' then
                ram_memory(to_integer(unsigned(addr_in))) <= di;
            end if;
            dout <= ram_memory(to_integer(unsigned(rd_addr)));
        end if;
    end process;

end Behavioral;

entity ssr_ram is 
    generic( 
        SSR:INTEGER:=16;
        DATA_WIDTH:INTEGER:=18;
        ADDR_WIDTH:INTEGER:=8);
    port(
        clk:in STD_LOGIC;
        ce:in STD_LOGIC:='1';
        
        -- write input and control
        di:in STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0);
        vi:in STD_LOGIC;
        addr_in:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);

        -- read control
        rd_addr_a:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        rd_addr_b:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        rd_addr_c:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        rd_addr_d:in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        
        out_a:out STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0);
        out_b:out STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0);
        out_c:out STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0);
        out_d:out STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0)
        );
end ssr_ram;

architecture Structural of ssr_ram is

    signal block_selector : STD_LOGIC_VECTOR(3 downto 0);
    signal write_baddress : STD_LOGIC_VECTOR(5 downto 0);

    type addr_array_t is array (0 to 3) of STD_LOGIC_VECTOR(5 downto 0);
    type data_array_t is array (0 to 3) of STD_LOGIC_VECTOR((SSR * DATA_WIDTH) - 1 downto 0);

    signal rd_addrs : addr_array_t;
    signal ram_outs : data_array_t;

begin

    rd_addrs(0) <= rd_addr_a(5 downto 0);
    rd_addrs(1) <= rd_addr_b(5 downto 0);
    rd_addrs(2) <= rd_addr_c(5 downto 0);
    rd_addrs(3) <= rd_addr_d(5 downto 0);

    out_a <= ram_outs(0);
    out_b <= ram_outs(1);
    out_c <= ram_outs(2);
    out_d <= ram_outs(3);

    write_baddress <= addr_in(5 downto 0);

    with addr_in(7 downto 6) select
        block_selector <= "0001" when "00",
                          "0010" when "01",
                          "0100" when "10",
                          "1000" when "11",
                          "0000" when others;

    gen_ram: for i in 0 to 3 generate
        u_ram_block: entity work.small_ram_block
            generic map (
                DEPTH      => 64,
                SSR        => SSR,
                DATA_WIDTH => DATA_WIDTH,
                ADDR_WIDTH => 6
            )
            port map (
                clk     => clk,
                ce      => ce,
                vi      => block_selector(i) and vi,
                di      => di,
                addr_in => write_baddress,
                rd_addr => rd_addrs(i),                
                dout    => ram_outs(i)
            );
    end generate gen_ram;

end Structural;
