import streamlit as st
import numpy as np
import pandas as pd
from libreria_funciones_proyecto1 import calcular_rotacion_inventario
from libreria_clases_proyecto1 import InventarioProducto

st.set_page_config(
    page_title="Proyecto Aplicado en Streamlit",
    layout="wide"
)

def mostrar_home():
    st.title("Proyecto Aplicado en Streamlit")
    st.subheader("Especialización en Python for Analytics")

    st.image("logoDMC.png", width=150)

    st.markdown("---")

    st.write("**Nombre completo:** Carla Sarmiento Prada")
    st.write("**Módulo:** Módulo 1 – Python Fundamentals")
    st.write("**Docente:** MSc. Carlos Carrillo Villavicencio")
    st.write("**Año:** 2026")

    st.markdown("---")

    st.subheader("Descripción del proyecto")
    st.write(
        "Esta aplicación integra los conceptos fundamentales del módulo: "
        "variables, estructuras de datos, control de flujo, funciones, "
        "programación funcional y programación orientada a objetos (POO)."
    )

def mostrar_ejercicio1():
    st.title("Ejercicio 1 - Flujo de Caja con Listas")
    st.markdown("Módulo para registrar movimientos financieros en una lista y calcular el saldo final.")
    st.markdown("---")

    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []

    st.subheader("Registrar movimiento")
    concepto = st.text_input("Concepto", placeholder="Ej: Venta de producto")
    tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
    valor = st.number_input("Valor (S/)", min_value=0.0, step=0.01)

    if st.button("Agregar movimiento"):
        if concepto == "":
            st.warning("Por favor ingresa un concepto.")
        elif valor == 0:
            st.warning("El valor debe ser mayor a 0.")
        else:
            movimiento = {"Concepto": concepto, "Tipo": tipo, "Valor": valor}
            st.session_state.movimientos.append(movimiento)
            st.success(f"Movimiento '{concepto}' agregado correctamente.")

    st.markdown("---")
    st.subheader("Movimientos registrados")

    if len(st.session_state.movimientos) == 0:
        st.info("Aún no hay movimientos registrados.")
    else:
        st.dataframe(st.session_state.movimientos, use_container_width=True)

        total_ingresos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
        total_gastos   = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
        saldo_final    = total_ingresos - total_gastos

        st.markdown("---")
        st.subheader("Resumen del flujo de caja")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", f"S/{total_ingresos:,.2f}")
        col2.metric("Total Gastos",   f"S/{total_gastos:,.2f}")
        col3.metric("Saldo Final",    f"S/{saldo_final:,.2f}")

        st.markdown("---")
        if saldo_final > 0:
            st.success(f"✅ El flujo de caja está A FAVOR con un saldo de S/{saldo_final:,.2f}")
        elif saldo_final < 0:
            st.error(f"❌ El flujo de caja está EN CONTRA con un saldo de S/{saldo_final:,.2f}")
        else:
            st.warning("⚖️ El flujo de caja está en EQUILIBRIO. Saldo = S/0.00")

def mostrar_ejercicio2():
    st.title("Ejercicio 2 – Registro con NumPy, Arrays y DataFrame")
    st.markdown("Formulario para registrar productos usando arreglos de NumPy y visualizarlos en un DataFrame.")
    st.markdown("---")

    # Inicializar arrays en session_state
    if "nombres" not in st.session_state:
        st.session_state.nombres    = np.array([])
        st.session_state.categorias = np.array([])
        st.session_state.precios    = np.array([])
        st.session_state.cantidades = np.array([])
        st.session_state.totales    = np.array([])

    # ── Formulario de ingreso ──
    st.subheader("Registrar producto")

    nombre    = st.text_input("Nombre del producto", placeholder="Ej: Laptop")
    categoria = st.selectbox("Categoría", ["Electrónica", "Ropa", "Alimentos", "Hogar", "Otro"])
    precio    = st.number_input("Precio unitario (S/)", min_value=0.0, step=0.01)
    cantidad  = st.number_input("Cantidad", min_value=1, step=1)
    total     = precio * cantidad
    st.write(f"**Total calculado:** S/{total:,.2f}")

    # ── Botón para agregar ──
    if st.button("Agregar producto"):
        if nombre == "":
            st.warning("Por favor ingresa el nombre del producto.")
        elif precio == 0:
            st.warning("El precio debe ser mayor a 0.")
        else:
            st.session_state.nombres    = np.append(st.session_state.nombres,    nombre)
            st.session_state.categorias = np.append(st.session_state.categorias, categoria)
            st.session_state.precios    = np.append(st.session_state.precios,    precio)
            st.session_state.cantidades = np.append(st.session_state.cantidades, cantidad)
            st.session_state.totales    = np.append(st.session_state.totales,    total)
            st.success(f"Producto '{nombre}' agregado correctamente.")

    st.markdown("---")

    # ── Tabla DataFrame ──
    st.subheader("Productos registrados")

    if len(st.session_state.nombres) == 0:
        st.info("Aún no hay productos registrados.")
    else:
        df = pd.DataFrame({
            "Producto"  : st.session_state.nombres,
            "Categoría" : st.session_state.categorias,
            "Precio"    : st.session_state.precios,
            "Cantidad"  : st.session_state.cantidades,
            "Total"     : st.session_state.totales
        })

        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("Resumen")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total productos registrados", len(st.session_state.nombres))
        col2.metric("Precio promedio",  f"S/{np.mean(st.session_state.precios):,.2f}")
        col3.metric("Total en ventas",  f"S/{np.sum(st.session_state.totales):,.2f}")

def mostrar_ejercicio3():
    st.title("Ejercicio 3 – Uso de Funciones desde Librería Externa")
    st.markdown("Cálculo de la **Rotación de Inventario**, indicador clave en Supply Chain y Planeamiento de Materiales.")
    st.markdown("---")

    # Inicializar histórico
    if "historico_ri" not in st.session_state:
        st.session_state.historico_ri = []

    # ── Descripción ──
    st.subheader("¿Qué calcula esta función?")
    st.write(
        "La rotación de inventario indica cuántas veces se renueva el stock en un periodo. "
        "Un valor alto significa que los materiales fluyen rápido, "
        "mientras que un valor bajo puede indicar sobrestock o materiales detenidos en almacén. "
        "También calcula los días promedio que un material permanece en inventario."
    )

    st.markdown("---")

    # ── Widgets de entrada ──
    st.subheader("Ingresar parámetros")

    costo_ventas       = st.number_input("Costo de ventas / consumo del periodo (S/)", min_value=0.01, step=100.0)
    inventario_inicial = st.number_input("Inventario inicial (S/)", min_value=0.0, step=100.0)
    inventario_final   = st.number_input("Inventario final (S/)", min_value=0.0, step=100.0)

    # ── Botón ejecutar ──
    if st.button("Calcular rotación de inventario"):
        try:
            resultado = calcular_rotacion_inventario(costo_ventas, inventario_inicial, inventario_final)

            st.success(f"✅ Rotación de inventario: {resultado['rotacion_inventario']:,.2f} veces")
            st.write(f"**Inventario promedio:** S/{resultado['inventario_promedio']:,.2f}")
            st.write(f"**Días promedio en inventario:** {resultado['dias_promedio_inventario']:,.2f} días")

            if resultado["dias_promedio_inventario"] <= 45:
                st.success("🟢 Inventario con alta rotación. Flujo eficiente de materiales.")
            elif resultado["dias_promedio_inventario"] <= 90:
                st.warning("🟡 Rotación moderada. Revisar niveles de stock.")
            else:
                st.error("🔴 Baja rotación. Posible sobrestock o materiales detenidos.")
            
            # Guardar en histórico
            st.session_state.historico_ri.append({
                "Costo Ventas (S/)"         : costo_ventas,
                "Inventario Inicial (S/)"   : inventario_inicial,
                "Inventario Final (S/)"     : inventario_final,
                "Inventario Promedio (S/)"  : resultado["inventario_promedio"],
                "Rotación (veces)"         : resultado["rotacion_inventario"],
                "Días en Inventario"       : resultado["dias_promedio_inventario"]
            })

        except ValueError as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    # ── Histórico ──
    st.subheader("Histórico de cálculos")

    if len(st.session_state.historico_ri) == 0:
        st.info("Aún no hay cálculos registrados.")
    else:
        import pandas as pd
        df_historico = pd.DataFrame(st.session_state.historico_ri)
        st.dataframe(df_historico, use_container_width=True)

        col1, col2 = st.columns(2)
        col1.metric("Cálculos realizados", len(st.session_state.historico_ri))
        col2.metric("Promedio días en inventario",
                    f"{df_historico['Días en Inventario'].mean():,.2f} días")
    
def mostrar_ejercicio4():
    st.title("Ejercicio 4 – Gestión de Inventario con Clases y CRUD")
    st.markdown("Módulo para gestionar productos en inventario usando la clase **InventarioProducto**.")
    st.markdown("---")

    # Inicializar inventario en session_state
    if "inventario" not in st.session_state:
        st.session_state.inventario = []

    # ── TABS ──
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Crear", "📋 Leer", "✏️ Actualizar", "🗑️ Eliminar"])

    # =========================================================
    # TAB 1 – CREAR
    # =========================================================
    with tab1:
        st.subheader("Registrar nuevo producto")

        nombre          = st.text_input("Nombre del producto", placeholder="Ej: Tornillo M8")
        costo_unitario  = st.number_input("Costo unitario (S/)", min_value=0.01, step=0.01)
        precio_unitario = st.number_input("Precio unitario (S/)", min_value=0.01, step=0.01)
        stock_actual    = st.number_input("Stock actual (unidades)", min_value=0, step=1)
        stock_minimo    = st.number_input("Stock mínimo (unidades)", min_value=0, step=1)

        if st.button("Agregar producto"):
            if nombre == "":
                st.warning("Por favor ingresa el nombre del producto.")
            else:
                try:
                    producto = InventarioProducto(
                        nombre, costo_unitario, precio_unitario, stock_actual, stock_minimo
                    )
                    st.session_state.inventario.append(producto.resumen())
                    st.success(f"✅ Producto '{nombre}' agregado correctamente.")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # =========================================================
    # TAB 2 – LEER
    # =========================================================
    with tab2:
        st.subheader("Inventario de productos")

        if len(st.session_state.inventario) == 0:
            st.info("Aún no hay productos registrados.")
        else:
            df = pd.DataFrame(st.session_state.inventario)
            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("Resumen")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total productos", len(df))
            col2.metric("Valor total inventario", f"S/{df['valor_inventario'].sum():,.2f}")
            col3.metric("Productos con reposición",
                int((df["necesita_reposicion"] == True).sum()))

            # Alertas de reposición
            productos_alerta = df[df["necesita_reposicion"] == True]["producto"].tolist()
            if productos_alerta:
                st.warning(f"⚠️ Productos que necesitan reposición: {', '.join(productos_alerta)}")
            else:
                st.success("✅ Todos los productos tienen stock suficiente.")

    # =========================================================
    # TAB 3 – ACTUALIZAR
    # =========================================================
    with tab3:
        st.subheader("Actualizar producto")

        if len(st.session_state.inventario) == 0:
            st.info("Aún no hay productos para actualizar.")
        else:
            nombres = [p["producto"] for p in st.session_state.inventario]
            seleccionado = st.selectbox("Selecciona el producto a actualizar", nombres)

            indice = nombres.index(seleccionado)
            producto_actual = st.session_state.inventario[indice]

            st.write(f"**Valores actuales de '{seleccionado}':**")
            col1, col2 = st.columns(2)
            col1.metric("Stock actual", f"{producto_actual['stock_actual']} uds")
            col1.metric("Valor inventario", f"S/ {producto_actual['valor_inventario']:.2f}")
            col2.metric("Margen unitario", f"S/ {producto_actual['margen_unitario']:.2f}")
            col2.metric("Margen %", f"{producto_actual['margen_pct']:.2f}%")

            st.markdown("---")
            st.write("**Nuevos valores:**")

            nuevo_costo   = st.number_input("Nuevo costo unitario (S/)",  min_value=0.01, step=0.01, key="upd_costo")
            nuevo_precio  = st.number_input("Nuevo precio unitario (S/)", min_value=0.01, step=0.01, key="upd_precio")
            nuevo_stock   = st.number_input("Nuevo stock actual",        min_value=0,    step=1,    key="upd_stock")
            nuevo_minimo  = st.number_input("Nuevo stock mínimo",        min_value=0,    step=1,    key="upd_minimo")

            if st.button("Actualizar producto"):
                try:
                    producto_actualizado = InventarioProducto(
                        seleccionado, nuevo_costo, nuevo_precio, nuevo_stock, nuevo_minimo
                    )
                    st.session_state.inventario[indice] = producto_actualizado.resumen()
                    st.success(f"✅ Producto '{seleccionado}' actualizado correctamente.")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # =========================================================
    # TAB 4 – ELIMINAR
    # =========================================================
    with tab4:
        st.subheader("Eliminar producto")

        if len(st.session_state.inventario) == 0:
            st.info("Aún no hay productos para eliminar.")
        else:
            nombres = [p["producto"] for p in st.session_state.inventario]
            seleccionado = st.selectbox("Selecciona el producto a eliminar", nombres, key="del_select")

            st.warning(f"⚠️ ¿Estás segura de que deseas eliminar '{seleccionado}'?")

            if st.button("Eliminar producto"):
                indice = nombres.index(seleccionado)
                st.session_state.inventario.pop(indice)
                st.success(f"🗑️ Producto '{seleccionado}' eliminado correctamente.")

# ── Menú lateral ──────────────────────────────
st.sidebar.image("LogoPersonal.png", width=120)
st.sidebar.title("Menú Principal")
busqueda = st.sidebar.text_input("🔍 Buscar sección")

secciones = ["🏠 Home", "📊 Ejercicio 1", "🔢 Ejercicio 2", "📦 Ejercicio 3", "🏭 Ejercicio 4"]

if busqueda:
    secciones_filtradas = [s for s in secciones if busqueda.lower().replace(" ", "") in s.lower().replace(" ", "")]
else:
    secciones_filtradas = secciones

if len(secciones_filtradas) == 0:
    st.sidebar.warning("No se encontró ninguna sección.")
    seccion = "Home"
else:
    seccion = st.sidebar.selectbox("Secciones:", secciones_filtradas)

# ── Enrutador ─────────────────────────────────
if seccion == "🏠 Home":
    mostrar_home()
elif seccion == "📊 Ejercicio 1":
    mostrar_ejercicio1()
elif seccion == "🔢 Ejercicio 2":
    mostrar_ejercicio2()
elif seccion == "📦 Ejercicio 3":
    mostrar_ejercicio3()
elif seccion == "🏭 Ejercicio 4":
    mostrar_ejercicio4()

